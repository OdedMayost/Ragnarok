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
import android.widget.Toast;

import java.io.IOException;
import java.net.Socket;

public class HomepageActivity extends AppCompatActivity {

    private static final String TAG = "ICT";
    String IP;
    Integer Port = 50000;
    Handler message_handler;
    String data_message;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getSupportActionBar().hide();
        setContentView(R.layout.activity_homepage);

        Intent homepage = getIntent();
        IP = homepage.getStringExtra("IP");
        Log.d(TAG, "IP = " + IP);

        message_handler = new Handler(Looper.getMainLooper()) {
            @Override
            public void handleMessage(Message message) {
                String receive = (String) message.obj;
                if (receive.length() >= 5){
                    data_message = receive.substring(5);
                    Log.d(TAG, "data message = " + data_message);
                    String [] data = data_message.split("~");
                    if (data[0].equals("START")){
                        if (data[1].equals("1")){
                            Intent bowling_game = new Intent(getApplicationContext(), BowlingGame.class);
                            bowling_game.putExtra("IP", IP);
                            startActivity(bowling_game);
                        }else if (data[1].equals("2")){
                            Intent rock_hero_game = new Intent(getApplicationContext(), RockHero.class);
                            rock_hero_game.putExtra("IP", IP);
                            startActivity(rock_hero_game);
                        }
                    }
                }
                Log.d(TAG, "Information received = " + data_message);
            }
        };
    }

    public void send_message(String data) {
        TcpBySize bg = new TcpBySize(this.message_handler, this.IP, this.Port);
        bg.execute(data);
    }

    public void arrow_up(View v){
        String message = "MOVES~1";
        send_message(message);
        Log.e(TAG, "move up");
    }

    public void arrow_down(View v){
        String message = "MOVES~2";
        send_message(message);
        Log.e(TAG, "move down");
    }

    public void choice(View v){
        String message = "CHOSE";
        send_message(message);
        Log.e(TAG, "move down");
    }
}