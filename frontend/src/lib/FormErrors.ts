export class FormErrors {
	shortPass: string = 'La contraseña es muy corta.';
	hasSpecials: string = 'Este campo no puede contener caracteres especiales o signos.';
	tooLong: string = 'Este campo excede el límite de caracteres';
	NotNumbers: string = 'La contraseña debe tener números.';
	NotValidEmail: string = 'Email no valido.';
	NotValidPhone: string = 'Telefono no valido. formato: +589999999999';
	NotUpperCase: string = 'La contraseña debe contener mayúsculas.';
	NotMatchingPass: string = 'Las contraseñas no coinciden.';
	SamePassword: string = 'La contraseña no puede ser igual a la anterior.';
    empyField: string = 'Este campo no puede estar vacío';
	hasUpperCase(str: string): boolean {
		return /[A-Z]/.test(str);
	}
	hasNumbers(str: string): boolean {
		return /\d/.test(str);
	}
	validateEmail(email: string): boolean {
		const emailRegex = /^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$/;
		return emailRegex.test(email);
	}
	validateText(text: string): boolean {
		const textRegex = /^[a-zA-Z0-9 ]+$/;
		return textRegex.test(text);
	}
	validatePhoneNumber(phone: string): boolean {
		if (phone.length < 1) return false;
		const phoneRegex = /^\+?58?\d{11,15}$/;
		return phoneRegex.test(phone);
	}
	validatePasswords(password: string, confirmPassword: string): boolean {
		return (
			password === confirmPassword &&
			password.length > 8 &&
			this.hasUpperCase(password) &&
			this.hasNumbers(password)
		);
	}
	validateCardID(cardID: string): boolean {
		if (cardID.length < 8 || cardID.length > 9) {
			return false;
		}
		const cardIDRegex = /^[VvEe][0-9]{8,9}$/;
		return cardIDRegex.test(cardID);
	}
}

export function getPassword(fields: any): string  {
	return fields.find((field: any) => field.name === 'password')?.value ?? '';
}
export function getConfirmPassword(fields: any): string  {
	return fields.find((field: any) => field.name === 'confirmPassword')?.value ?? '';
}

export function getEmail(fields: any): string  {
	return fields.find((field: any) => field.name === 'email')?.value ?? '';
}

export function getPhonenumber(fields: any): string {
	return fields.find((field: any) => field.name === 'phonenumber')?.value ?? '';
}
export function getName(fields: any): string {
	return fields.find((field: any) => field.name === 'name')?.value ?? '';
}

export function getCardID(fields: any): string {
	return fields.find((field: any) => field.name === 'card_id')?.value ?? '';
}

export function getAddress(fields: any): string {
	return fields.find((field: any) => field.name === 'address')?.value ?? '';
}