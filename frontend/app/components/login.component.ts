import { Component, EventEmitter, Output } from '@angular/core';
import { AuthService } from '../services/auth.service';

@Component({
    selector: 'login',
    templateUrl: './app/templates/login.template.html'
})
export class LoginPage { 
  @Output() onAuthenticated = new EventEmitter<Object>();

  private user = {
    email: "",
    password: "",
  }

  constructor(private authService: AuthService) { }

  login() {
   
   //this.onAuthenticated.emit(this.user);

    this.authService.login(this.user).subscribe(
        () => this.onAuthenticated.emit(true)
    );
  }


}

