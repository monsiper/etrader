import { Component } from '@angular/core'
import { Http } from '@angular/http'

@Component({
  selector: 'dashboard',
  templateUrl: './app/templates/dashboard.template.html'
})
export class Dashboard implements OnInit {

  private arrayOfKeys: Array<string>;
  private prices = {
    usd: 20
  }

  getPrices() {
    console.log("getting prices");
    this.http.get("https://coinmarketcap-nexuist.rhcloud.com/api/eth")
      .map(
        resp => resp.json()
      )
      .subscribe(
        resp => {
          console.log(resp);
          this.prices = resp['price'];
          this.arrayOfKeys = Object.keys(this.prices);
          console.log(resp);
        }
      );
  }

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

  ngOnInit() {
    console.log("init");
    this.loadwidget();
    this.getPrices();
    this.arrayOfKeys = Object.keys(this.prices);
  }

  constructor(private http: Http) {
    this.loadwidget();
    this.getPrices();
    this.arrayOfKeys = Object.keys(this.prices);

  }

  
}
