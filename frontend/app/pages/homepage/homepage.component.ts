import { Component, EventEmitter, Output } from '@angular/core';

@Component({
    selector: 'login',
    templateUrl: './app/pages/homepage/homepage.template.html',
    styleUrls: ['./app/pages/homepage/homepage.styles.css']
})
export class LoginPage { 
  @Output() onAuthenticated = new EventEmitter<boolean>();

  private email: string;
  private password: string;

  authenticateUser() {
    this.onAuthenticated.emit(true);
  }


}

