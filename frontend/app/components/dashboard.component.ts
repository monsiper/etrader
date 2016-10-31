import { Component } from '@angular/core'

@Component({
  selector: 'dashboard',
  templateUrl: './app/templates/dashboard.template.html'
})
export class Dashboard {

  loadwidget() {
    !function(d,s,id) {
      let js, fjs=d.getElementsByTagName(s)[0], p=/^http:/.test(d.location.toString())?'http':'https';
      if(!d.getElementById(id)) {
        js=d.createElement(s);
        js.id=id;
        js.src=p+"://platform.twitter.com/widgets.js";
        fjs.parentNode.insertBefore(js,fjs);
      }
    }
    (document,"script","twitter-wjs");
  }

  constructor() {
    this.loadwidget();
  }
}
