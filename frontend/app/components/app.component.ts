import { Component }      from '@angular/core';
import { Http, Headers } from '@angular/http';
import { LoginPage } from './login.component';
import { AuthService } from '../services/auth.service';

@Component({
    selector: 'my-app',
    templateUrl: './app/templates/app.template.html',
    styleUrls: ['./app/styles/app.styles.css'],
    providers: [AuthService]
})
export class ETrader { 

  // todo: if login replace tabs with login?
  // if not logged in disable other two tabs
  // css for tabs
  //

  
  private isAuthenticated = false;
  private dashboard = false;
  private profile = true;
  private trade = false;
	private user = {
    user_name: "",
    password: "",
  }

  activate(i) {
    console.log(i);

    switch(i) {
      case 1:
        this.dashboard = true;
        this.profile = false;
        this.trade = false;
        break;
     case 2:
        this.dashboard = false;
        this.profile = true;
        this.trade = false;
        break;
     case 3:
        this.dashboard = false;
        this.profile = false;
        this.trade = true;
        break;
     default:
       this.dashboard = true;
       this.profile = false;
       this.trade = false;
       break;
    }
  }

  onAuthenticated(user) {
    this.user = user;
    this.isAuthenticated = true;
  }

  signOut() {
    this.user = null;
    this.isAuthenticated = false;
  }
}

