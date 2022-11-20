package com.example.ragnarokapp;

import android.os.AsyncTask;
import android.os.Handler;
import android.os.Message;
import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class TcpBySize extends AsyncTask<String, Handler,Void> {
    String IP;
    Integer Port;
    PrintWriter pw;
    final static int LEN_SIZE = 4;

    public TcpBySize(Handler MessageHandler, String IP, Integer Port) {
        if (IP != "")
            this.IP = IP;
        if (Port != null)
            this.Port = Port;
        Socket socket = SocketHandler.getSocket();
        Handler handler = SocketHandler.getHandlerReceiver();
        if (handler != MessageHandler)        {
            SocketHandler.setHandlerReceiver(MessageHandler);
        }
    }

    @Override
    protected Void doInBackground(String... voids) {
        String TAG = "doInBackground";
        Socket socket = SocketHandler.getSocket();

        if (socket == null) {
            try {
                Log.d(TAG, "Before Connect");
                socket = new Socket(this.IP, this.Port);
                SocketHandler.setSocket(socket);

                Log.d(TAG, "connected");
                Thread listener = new Thread(new Listener(socket));
                listener.start();

            } catch (UnknownHostException e) {
                Log.e(TAG, "ERROR UnknownHostException socket");

            } catch (IOException e) {
                Log.e(TAG, "ERROR IOException socket " +e.toString());
            }
        }

        String data = voids[0];
        data = String.format("%04d", data.length()) + "|" + data;
        Log.d(TAG, "Before Send 1");
        try {
            pw = new PrintWriter(socket.getOutputStream());
            Log.d(TAG, "Before Send 2");
            pw.write(data);
            pw.flush();
            Log.d(TAG, "After Send:" + data);

        } catch (IOException e) {
            Log.e(TAG, "ERROR write " + e.getMessage());
            Handler MessageHandler = SocketHandler.getHandlerReceiver();
            Message message = MessageHandler.obtainMessage();
            message.obj = "Socket Error";
            MessageHandler.sendMessage(message);
        }
        return null;
    }

    class Listener implements Runnable {
        String TAG = "Listener";
        Socket socket_listener;
        BufferedReader input;
        char[] char_buffer;

        public Listener(Socket socket) {
            this.socket_listener = socket;

            try {
                this.input = new BufferedReader(new InputStreamReader(this.socket_listener.getInputStream()));
            } catch (IOException e) {
                Log.e(TAG, "ERROR buffer read " + e.getMessage());
                e.printStackTrace();
            }

            char_buffer = new char[2000];
        }

        @Override
        public void run() {
            boolean state = true;
            while (state) {
                try {
                    if (input.ready()) {
                        int length_read = 0;
                        char[] char_buffer_length = new char[LEN_SIZE];

                        while (length_read < LEN_SIZE){
                            length_read += input.read(char_buffer_length, 0, LEN_SIZE-length_read);
                        }
                        String received_length = new String(char_buffer_length, 0, LEN_SIZE);
                        int total_to_read = Integer.parseInt(received_length);

                        int length = input.read(char_buffer, 0, total_to_read +1);
                        String received = received_length + new String(char_buffer, 0, length) ;
                        length += LEN_SIZE;
                        if (length > 0) {
                            Log.d(TAG, "got data: " + received );

                            Handler MessageHandler = SocketHandler.getHandlerReceiver();
                            if (MessageHandler == null)
                            {
                                try{
                                    Thread.sleep(2000);
                                } catch (InterruptedException e) {
                                    e.printStackTrace();
                                }
                                MessageHandler = SocketHandler.getHandlerReceiver();
                            }
                            if (MessageHandler == null)
                            {
                                try{
                                    Thread.sleep(2000);
                                } catch (InterruptedException e) {
                                    e.printStackTrace();
                                }
                                MessageHandler = SocketHandler.getHandlerReceiver();
                            }

                            if (MessageHandler != null){
                                Message message = MessageHandler.obtainMessage();
                                message.obj = received;
                                MessageHandler.sendMessage(message);
                            }
                            else{
                                Log.e(TAG, "Handle = Null skipping message = " + received);
                            }

                        }
                    }
                } catch (IOException e) {
                    Log.e(TAG, "ERROR read line - " + e.getMessage());
                    e.printStackTrace();
                    state = false;
                }

                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Log.e(TAG, "ERROR InterruptedException " + e.getMessage());
                    e.printStackTrace();
                }
            }
            Log.d(TAG, "Login Listener finished ");
        }
    }
}
