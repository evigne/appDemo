import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { DialogConfirmComponent } from 'src/app/components/dialog-confirm/dialog-confirm.component';

interface TreeNode {
  name: string;
  created_at: Date;
  properties: { key: string; value: string; created_at: Date }[];
  children?: TreeNode[];
}

@Component({
  selector: 'app-card',
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.css'],
})
export class CardComponent implements OnChanges {
  constructor(public dialog: MatDialog) {}
  @Input() subtree: TreeNode[] | undefined;

  getPropColor(value: string): string {
    return parseFloat(value) > 10 ? 'green' : 'inherit';
  }

  ngOnChanges(changes: SimpleChanges) {
    console.log('Subtree changed in ComponentB', this.subtree);
  }

  openConfirmDialog(): void {
    const dialogRef = this.dialog.open(DialogConfirmComponent);

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        console.log('Result', result);
      }
    });
  }
}
