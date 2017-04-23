/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package reportes_edd;

/**
 *
 * @author ricar
 */
import WebService.WebService;
import GUI.Principal;
import javax.swing.*;
public class Reportes_EDD {
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        WebService ser = new WebService();
        if(ser.conectarAWebService().equals("Conexion Correcta con Java y Django")){
            JOptionPane.showMessageDialog(null,"Conexión Establecida");
            Principal ventana = new Principal();
            ventana.setVisible(true);
        }
        else{
            JOptionPane.showConfirmDialog(null, "Conexión Fallida...");
        }
        
    }
    
}
