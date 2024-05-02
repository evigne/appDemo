import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Subject, of } from 'rxjs';
import { debounceTime, switchMap, catchError } from 'rxjs/operators';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-input',
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.css'],
})
export class InputComponent implements OnInit {
  private searchTerms = new Subject<string>();
  subtree: any;
  constructor(private http: HttpClient) {}
  onKey(event: KeyboardEvent) {
    const inputElement = event.target as HTMLInputElement;
    const inputValue = inputElement.value;
    if (inputValue.trim()) {
      this.searchTerms.next(inputValue.trim());
    } else {
      this.subtree = [];
    }
  }

  ngOnInit(): void {
    this.searchTerms
      .pipe(
        debounceTime(200),
        switchMap(
          (path: string) =>
            this.http.get(`http://127.0.0.1:5000/get_subtree/${path}`).pipe(
              catchError((error) => {
                console.error('Error fetching data:', error);
                this.subtree = [];
                return of([]);
              })
            )

          // this.http.get(`${environment.BACKEND_URL}/get_subtree/${path}`)
        )
      )
      .subscribe((data) => {
        this.subtree = data;
        console.log('Data', data);
      });
  }
}
