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
import com.squareup.okhttp.FormEncodingBuilder;
import com.squareup.okhttp.RequestBody;
import javax.swing.*;
public class Reportes_EDD {
    /**
     * @param args the command line arguments
     */
    static WebService servicio = new WebService();
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
        /*RequestBody formBody = new FormEncodingBuilder()
                .add("nombre", "android")
                .add("contraseña","1234")
                .build();
        String re = servicio.realizarOperacion("Drive/Android/Registrar", formBody).toString();
        System.out.println(re);*/
    }
    
}
