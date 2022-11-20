package com.example.ragnarokapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.widget.TextView;

import java.io.IOException;
import java.math.BigInteger;
import java.net.Socket;
import java.util.Random;

public class StartupActivity extends AppCompatActivity {

    private static final String TAG = "ICT";
    String IP = "172.20.10.6";
    Integer Port = 55555;
    Handler message_handler;
    String data_message;
    Integer connection_type;
    String computer_ip;

    int a;
    BigInteger p;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getSupportActionBar().hide();
        setContentView(R.layout.activity_startup);

        message_handler = new Handler(Looper.getMainLooper()) {
            @Override
            public void handleMessage(Message message) {
                String receive = (String) message.obj;
                if (receive.length() >= 5){
                    data_message = receive.substring(5);
                    Log.d(TAG, "data message = " + data_message);
                    Log.d(TAG, "connection type = " + connection_type);
                    String [] data = data_message.split("~");
                    if (data[0].equals("COMIP")) {
                        diffieHellman();
                        computer_ip = data[1];
                    } else if (data[0].equals("DIFHL")){
                        BigInteger B = new BigInteger(data[1]);
                        BigInteger K = B.pow(a).mod(p);
                        String key = K.toString().substring(0, 16);
                        if (!computer_ip.equals("") && (connection_type != null)) {
                            if (connection_type == 1) {
                                Intent signin_activity = new Intent(getApplicationContext(), SignInActivity.class);
                                signin_activity.putExtra("IP", computer_ip);
                                signin_activity.putExtra("Key", key);
                                startActivity(signin_activity);
                            } else if (connection_type == 2) {
                                Intent signup_activity = new Intent(getApplicationContext(), SignUpActivity.class);
                                signup_activity.putExtra("IP", computer_ip);
                                signup_activity.putExtra("Key", key);
                                startActivity(signup_activity);
                            }
                        }
                    }
                }
                Log.d(TAG, "data received = " + data_message);
            }
        };
    }

    public void sign_in(View v){
        connection_type = 1;
        String computer_id = ((TextView) findViewById(R.id.Computer_ID)).getText().toString();
        String message = "COMID~" + computer_id;
        send_message(message);
        Log.d(TAG, "data sent = " + message);
    }

    public void sign_up(View v){
        connection_type = 2;
        String computer_id = ((TextView) findViewById(R.id.Computer_ID)).getText().toString();
        String message = "COMID~" + computer_id;
        send_message(message);
        Log.d(TAG, "data sent = " + message);
    }

    public void diffieHellman() {
        Random rnd = new Random();
        p = new BigInteger("23889941541091598209");
        BigInteger g = new BigInteger("12987747831457530552");
        a = rnd.nextInt(40000) + 10000;
        BigInteger A = g.pow(a).mod(p);
        String message = String.format("DIFHL~%s~%s~%s", A, p, g);
        send_message(message);
    }

    public void send_message(String data) {
        Socket sk = SocketHandler.getSocket();
        if (sk != null) {
            try {
                sk.close();
                SocketHandler.setSocket(null);

            } catch (IOException e) {
                Log.e(TAG, "ERROR IOException close socket");
            }
        }

        TcpBySize bg = new TcpBySize(this.message_handler, this.IP, this.Port);
        bg.execute(data);
    }
}