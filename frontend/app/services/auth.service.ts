import { Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http';

@Injectable()
export class AuthService {

  constructor(private http: Http) { }

  login(user) {
    let headers = new Headers();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    return this.http.post('http://localhost:8000/login', user, { headers: headers })
						.map(response => response.json()); 
  }

  register(user) {
    let headers = new Headers();
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    return this.http.post('http://localhost:8000/register', user, { headers: headers })
						.map(response => response.json()); 
  }
}
