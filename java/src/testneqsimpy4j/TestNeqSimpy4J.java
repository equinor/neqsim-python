/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package testneqsimpy4j;

import py4j.GatewayServer;

/**
 *
 * @author ESOL
 */
public class TestNeqSimpy4J {

    public double addDouble(){
        return 1.0;
    }
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        TestNeqSimpy4J app = new TestNeqSimpy4J();
        // app is now the gateway.entry_point
        GatewayServer server = new GatewayServer(app);
        server.start();
    }

}
