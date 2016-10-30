import { NgModule, Component }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { ETrader } from './app.component';
import { LoginPage } from './pages/homepage/homepage.component';


@NgModule({
  imports:      [ BrowserModule ],
  declarations: [ ETrader, LoginPage ],
  bootstrap:    [ ETrader ]
})
export class AppModule { 


  constructor() { }
}

