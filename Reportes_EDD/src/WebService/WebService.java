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
import com.squareup.okhttp.OkHttpClient;
import com.squareup.okhttp.Request;
import com.squareup.okhttp.RequestBody;
import com.squareup.okhttp.Response;

import java.net.MalformedURLException;
import java.net.URL;

public class WebService {
    public static OkHttpClient webClient = new OkHttpClient();
    URL url;
    Request request;
    Response response;
    
    public WebService(){
        //CONSTRUCTOR DE CONEXIÓN AL SERVIDOR WEB
    }
    
    public Object realizarOperacion(String metodo, RequestBody body){
        Object retorno = null;
        String pr = "";
        try{
           //System.out.println("ESTOY EN METODO "+metodo);
           url = new URL("http://0.0.0.0:8000/"+metodo);
           request = new Request.Builder().url(url).post(body).build();
           response = webClient.newCall(request).execute();
           retorno = response.body().string();
        }
        catch(Exception e){
            System.out.println("Ocurrio un Error en Metodo: "+metodo);
        }
        return retorno;
    }
    
    public Object consultar(String metodo){
        Object retorno = null;
        try{
            url = new URL("http://0.0.0.0:8000/"+metodo);
            request = new Request.Builder().url(url).build();
            response = webClient.newCall(request).execute();
            retorno = response.body().string();
        }
        catch(Exception e){
            System.out.println("Hubo Error al realizar consulta al metodo: "+metodo);
        }
        return retorno;
    }
    
    public String conectarAWebService(){
        String confirmacion = "";
        try{
            url = new URL("http://0.0.0.0:8000/Conectar");
            request = new Request.Builder().url(url).build();
            response = webClient.newCall(request).execute();
            confirmacion = response.body().string();
        }
        catch(Exception e){
            confirmacion = "Conección Fallida a Web Service";
        }
        return confirmacion;
    }
}
