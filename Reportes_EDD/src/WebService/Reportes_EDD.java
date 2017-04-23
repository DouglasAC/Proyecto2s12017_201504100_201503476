/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package WebService;

/**
 *
 * @author ricar
 */
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Reportes_EDD {
    String ruta;
    public Reportes_EDD(){
        //CONSTRUCTOR POR DEFECTO
    }
    
    public void crearDot(String nombre, String texto){
        System.out.println("Arhivo Creado");
        ruta = "C:/Reportes_EDD_2/"+nombre+".txt";
        File f;
        FileWriter escribir;
        try{
            File c = new File(".");
            f = new File(ruta);
            escribir = new FileWriter(f);
            BufferedWriter bw = new BufferedWriter(escribir);
            PrintWriter salida = new PrintWriter(bw);
            salida.write(texto);
            salida.close();
            bw.close();
            generarImagen(nombre);
            escribirHTML(nombre);
        }
        catch(Exception e){
            
        }
        
    }
    
    private void generarImagen(String nombre){
        File f = new File(".");
        
            String dotPath ="C:\\Program Files (x86)\\Graphviz2.38\\bin\\dot.exe";
            String fileOut = "C:\\Reportes_EDD_2\\"+nombre+".png";
            String param = "-Tpng";
            String input = "C:\\Reportes_EDD_2\\"+nombre+".txt";
            String toP = "-o";
            String[] cmd = new String[5];
            cmd[0] = dotPath;
            cmd[1] = param;
            cmd[2] = input;
            cmd[3] = toP;
            cmd[4] = fileOut;
            Runtime rt = Runtime.getRuntime();
            
        try {
            rt.exec(cmd);
        } catch (IOException ex) {
            Logger.getLogger(Reportes_EDD.class.getName()).log(Level.SEVERE, null, ex);
        }
        
    }
    private void escribirHTML(String nombre){
        File f;
        FileWriter escribir;
        try{
            f = new File("C:\\Reportes_EDD_2\\"+nombre+".html");
            escribir = new FileWriter(f);
            BufferedWriter bw = new BufferedWriter(escribir);
            PrintWriter salida = new PrintWriter(bw);
            salida.write("<!DOCTYPE html>\n" +
    "<html lang='en'>\n" +
    "  <head>\n" +
    "    <meta charset='utf-8'>\n" +
    "    <meta http-equiv='X-UA-Compatible' content='IE=edge'>\n" +
    "    <meta name='viewport' content='width=device-width, initial-scale=1'>\n" +
    "    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->\n" +
    "    <title>DEFAULT VIEW</title>\n" +
    "\n" +
    "  </head>\n" +
    "  <body bgcolor='#D8D8D8'>\n" +
    "  <center><img src='"+nombre+".png'></center>\n" +
    "  </body>\n" +
    "</html>");
            salida.close();
            bw.close();
        }
        catch(Exception Ex){
            
        }
    }
}
