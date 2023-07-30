import styles from 'css/OrdinalColors.module.css';

export function getOrdinal(number: number): string {
  const suffixes = ['th', 'st', 'nd', 'rd'];
  const v = number % 100;
  return number + (suffixes[(v - 20) % 10] || suffixes[v] || suffixes[0]);
};

export function addPlacementClass(ordinal: string): string {
  if (ordinal === "1st") {
    return styles.firstPlace;
  } else if (ordinal === "2nd") {
    return styles.secondPlace;
  } else if (ordinal === "3rd") {
    return styles.thirdPlace;
  } else {
    return "";
  }
};

export function formatDatetime(datetime: string): string {
  const dateObject: Date = new Date(datetime);
  const dateString: string = dateObject.toLocaleString([], {dateStyle: 'medium', timeStyle: 'long'});
  return dateString;
};