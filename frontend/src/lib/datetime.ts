export function getCurrentDateTime(): string {
	const now = new Date();

	const year = now.getFullYear();
	const month = String(now.getMonth() + 1).padStart(2, '0');
	const day = String(now.getDate()).padStart(2, '0');
	const hours = String(now.getHours()).padStart(2, '0');
	const minutes = String(now.getMinutes()).padStart(2, '0');
	const seconds = String(now.getSeconds()).padStart(2, '0');
	const milliseconds = String(now.getMilliseconds()).padStart(3, '0').padEnd(6, '0');
	const timezoneOffset = now.getTimezoneOffset();
	const offsetHours = String(Math.abs(timezoneOffset / 60)).padStart(2, '0');
	const offsetMinutes = String(Math.abs(timezoneOffset % 60)).padStart(2, '0');
	const offsetSign = timezoneOffset > 0 ? '-' : '+';
	return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}.${milliseconds}${offsetSign}${offsetHours}:${offsetMinutes}`;
}
export function formatDateTime(timestamp: string): string {
	const date = new Date(timestamp);
	// Return only the date portion (adjust format as needed)
	return date.toLocaleDateString('es', {
		year: 'numeric',
		month: 'long',
		day: 'numeric',
		hour: '2-digit',
		minute: '2-digit'
	});
}
export function convertDateToTimestamp(d: string) {
	if (!d) return '';
	// Por ejemplo, asumiendo que se quiere iniciar a medianoche local
	const dt = new Date(d + 'T00:00:00');
	// Si necesitas ajustar la zona horaria, agrega la lógica necesaria.
	return dt.getTime().toString();
}
