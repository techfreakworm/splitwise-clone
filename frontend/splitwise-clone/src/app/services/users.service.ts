import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { interval, firstValueFrom } from 'rxjs';



@Injectable({
  providedIn: 'root'
})
export class UsersService {

  constructor(public http: HttpClient) { }

  get_users(){
   return this.http.get(`${environment.api}/user`)
    
  }
}
