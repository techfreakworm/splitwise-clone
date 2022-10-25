import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {MaterialImportModule} from './material.module';
import { CurrentUserComponent } from './components/current-user/current-user.component';
import { GroupsTableComponent } from './components/groups-table/groups-table.component';
import { ExpensesTableComponent } from './components/expenses-table/expenses-table.component';
import { UserFormComponent } from './components/user-form/user-form.component';
import { ExpenseFormComponent } from './components/expense-form/expense-form.component';
import { UserTableComponent } from './components/user-table/user-table.component';
import { GroupsFormComponent } from './components/groups-form/groups-form.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    AppComponent,
    CurrentUserComponent,
    GroupsTableComponent,
    ExpensesTableComponent,
    UserFormComponent,
    ExpenseFormComponent,
    UserTableComponent,
    GroupsFormComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MaterialImportModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
