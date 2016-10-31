import { NgModule, Component }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { FormsModule } from '@angular/forms';
import { HttpModule, JsonpModule } from '@angular/http';

import 'rxjs/add/operator/map';
import 'rxjs/add/operator/toPromise';

import { ETrader } from './components/app.component';
import { LoginPage } from './components/login.component';
import { Dashboard } from './components/dashboard.component';

@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    JsonpModule
  ],
  declarations: [ ETrader, LoginPage, Dashboard ],
  bootstrap:    [ ETrader ]
})
export class AppModule { 
  constructor() { }
}

