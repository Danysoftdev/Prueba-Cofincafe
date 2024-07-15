import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MatTableDataSource } from '@angular/material/table';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  datosTabla = new MatTableDataSource<any>([]);
  columnas: string[] = ['NIT', 'Nombre', 'Ingresos', 'Egresos', 'Total'];
  estadisticas: any = {};
  cargando = false;

  constructor(private http: HttpClient) {}

  cargarInfo() {
    this.cargando = true;
    this.http.get('http://localhost:5000/datos').subscribe(
      (response: any) => {
        this.datosTabla.data = response.datos;
        this.estadisticas = response.estadisticas;
        this.cargando = false;
      },
      error => {
        console.error(error);
        this.cargando = false;
      }
    );
  }

}
