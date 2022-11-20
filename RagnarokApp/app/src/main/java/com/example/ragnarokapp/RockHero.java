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

public class RockHero extends AppCompatActivity {

    private static final String TAG = "ICT";
    String IP;
    Integer Port = 50000;
    Handler message_handler;
    String data_message;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getSupportActionBar().hide();
        setContentView(R.layout.activity_rock_hero);

        Intent boxing_game = getIntent();
        IP = boxing_game.getStringExtra("IP");
        Log.d(TAG, "IP = " + IP);

        message_handler = new Handler(Looper.getMainLooper()) {
            @Override
            public void handleMessage(Message message) {
                String receive = (String) message.obj;
                if (receive.length() >= 5){
                    data_message = receive.substring(5);
                    if (data_message.equals("ENDED")){
                        Intent homepage = new Intent(getApplicationContext(), HomepageActivity.class);
                        homepage.putExtra("IP", IP);
                        startActivity(homepage);
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

    public void arrow_right(View view){
        String message = "PRESS~1";
        send_message(message);
        Log.e(TAG, "move right");
    }

    public void arrow_left(View view){
        String message = "PRESS~2";
        send_message(message);
        Log.e(TAG, "move left");
    }

    public void arrow_up(View v){
        String message = "PRESS~3";
        send_message(message);
        Log.e(TAG, "move up");
    }

    public void arrow_down(View v){
        String message = "PRESS~4";
        send_message(message);
        Log.e(TAG, "move down");
    }

}