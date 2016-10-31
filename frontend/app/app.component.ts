import { Component }      from '@angular/core';

import { LoginPage } from './pages/homepage/homepage.component';
@Component({
    selector: 'my-app',
    templateUrl: './app/app.template.html',
    styleUrls: ['./app/pages/homepage/homepage.styles.css']
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

  onAuthenticated(value) {
    console.log("true");
    this.isAuthenticated = true;
  }
}

