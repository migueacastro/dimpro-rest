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
    // Limpiar espacios y convertir a mayúsculas
    const cleanedID = cardID.trim().toUpperCase();

    // Verificar longitud total (7-11 caracteres)
    if (cleanedID.length < 7 || cleanedID.length > 11) {
        return false;
    }

    // Validar RIF (ej: J-1234567-1, J12345671, G1234567)
    const rifRegex = /^[VEJGPCR](-?[0-9]{4,9}-?[0-9]?)$/;
    if (rifRegex.test(cleanedID)) {
        const digitsOnly = cleanedID.replace(/[^0-9]/g, "");
        return digitsOnly.length >= 6 && digitsOnly.length <= 10;
    }

    // Validar cédula (ej: V12345678, E123456789, V-1234567)
    const cedulaRegex = /^[VE](-?[0-9]{6,9})$/;
    if (cedulaRegex.test(cleanedID)) {
        const digitsOnly = cleanedID.replace(/[^0-9]/g, "");
        return digitsOnly.length >= 7 && digitsOnly.length <= 9;
    }

    return false;
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