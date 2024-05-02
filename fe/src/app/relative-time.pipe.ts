import { Pipe, PipeTransform } from '@angular/core';
import { parseISO, formatDistanceToNow } from 'date-fns';

@Pipe({
  name: 'relativeTime',
})
export class RelativeTimePipe implements PipeTransform {
  transform(createdAt: Date): string {
    const now = new Date();
    const created = new Date(createdAt);
    const elapsedMilliseconds = now.getTime() - created.getTime();

    // Convert milliseconds to seconds
    const elapsedSeconds = Math.floor(elapsedMilliseconds / 1000);

    // Define time units
    const minute = 60;
    const hour = 60 * minute;
    const day = 24 * hour;

    if (elapsedSeconds < minute) {
      return `${elapsedSeconds} second${elapsedSeconds === 1 ? '' : 's'} ago`;
    } else if (elapsedSeconds < hour) {
      const minutes = Math.floor(elapsedSeconds / minute);
      return `${minutes} minute${minutes === 1 ? '' : 's'} ago`;
    } else if (elapsedSeconds < day) {
      const hours = Math.floor(elapsedSeconds / hour);
      return `${hours} hour${hours === 1 ? '' : 's'} ago`;
    } else {
      const days = Math.floor(elapsedSeconds / day);
      return `${days} day${days === 1 ? '' : 's'} ago`;
    }
  }
}
