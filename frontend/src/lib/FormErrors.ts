export class FormErrors{
    shortPass: string = "La contraseña es muy corta.";
    NotNumbers: string = "La contraseña debe tener números.";
    NotValidEmail: string = "Email no valido.";
    NotUpperCase: string = "La contraseña debe contener mayúsculas.";
    NotMatchingPass: string = "Las contraseñas no coinciden.";
    hasUpperCase(str: string): boolean {
        return /[A-Z]/.test(str);
    }
    hasNumbers(str: string): boolean {
        return /\d/.test(str);
    }
    validateEmail(email:string ): boolean {
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return emailRegex.test(email)
    }
    validatePasswords(password:string, confirmPassword:string): boolean {
        return (password===confirmPassword && password.length>5 && this.hasUpperCase(password) && this.hasNumbers(password))
    }
}