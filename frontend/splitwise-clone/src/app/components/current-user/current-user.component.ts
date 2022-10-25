import { ChangeDetectorRef, Component, OnDestroy, OnInit } from '@angular/core';
import { Subscribable, Subscription } from 'rxjs';
import { UsersService } from 'src/app/services/users.service';
import {MatSelectModule} from '@angular/material/select';


@Component({
  selector: 'app-current-user',
  templateUrl: './current-user.component.html',
  styleUrls: ['./current-user.component.scss']
})
export class CurrentUserComponent implements OnInit,OnDestroy {
  users : any
  currentUser = ''
  subscription: Subscription | undefined
  
  constructor(public usersService: UsersService,public changeDetectorRef: ChangeDetectorRef) { }
  

  ngOnInit(): void {
    // this.users = []
    this.subscription = this.usersService.get_users().subscribe((data: any) => {
      this.users = data
      // console.log(data)
      // data.forEach((element: any) => {
      //   this.users.push(element['username'])
      // });
      // this.changeDetectorRef.detectChanges()
      // console.log(this.users)
    })
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe()
  }

  changeUser(username: string) {
    this.currentUser = username
    console.log(this.currentUser)
  }

}
