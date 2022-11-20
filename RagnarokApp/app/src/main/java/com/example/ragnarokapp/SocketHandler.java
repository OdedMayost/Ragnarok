package com.example.ragnarokapp;

import android.os.Handler;
import java.net.Socket;

public class SocketHandler {
    private static Socket socket;
    private static Handler HandlerReceiver;

    public static synchronized Socket getSocket(){
        return socket;
    }

    public static synchronized void setSocket(Socket socket){
        SocketHandler.socket = socket;
    }

    public static synchronized Handler getHandlerReceiver(){
        return HandlerReceiver;
    }

    public static synchronized void setHandlerReceiver(Handler HandlerReceiver){
        SocketHandler.HandlerReceiver = HandlerReceiver;
    }
}
