package com.example.ragnarokapp;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.widget.TextView;
import android.widget.Toast;

import java.io.IOException;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.security.InvalidKeyException;
import java.security.Key;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.spec.SecretKeySpec;

public class SignInActivity extends AppCompatActivity {

    private static final String TAG = "ICT";
    String IP;
    Integer Port = 50000;
    Handler message_handler;
    String data_message;
    byte [] Key;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getSupportActionBar().hide();
        setContentView(R.layout.activity_sign_in);

        Intent signin_activity = getIntent();
        IP = signin_activity.getStringExtra("IP");
        Log.d(TAG, "IP = " + IP);
        Key = signin_activity.getStringExtra("Key").getBytes();
        Log.d(TAG, "Key = " + Key.toString());

        message_handler = new Handler(Looper.getMainLooper()) {
            @Override
            public void handleMessage(Message message) {
                String receive = (String) message.obj;
                if (receive.length() >= 5) {
                    data_message = receive.substring(5);
                    String[] data = data_message.split("~");
                    if (data[0].equals("LOGIN")) {
                        if (data[1].equals("1")) {
                            Intent homepage = new Intent(getApplicationContext(), HomepageActivity.class);
                            homepage.putExtra("IP", IP);
                            startActivity(homepage);
                        } else if (data[1].equals("2")) {
                            String error = "Error: Login failed";
                            Toast.makeText(getApplicationContext(), error, Toast.LENGTH_SHORT).show();
                        }
                    }
                }
                Log.d(TAG, "Information received = " + data_message);
            }
        };
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

    @RequiresApi(api = Build.VERSION_CODES.O)
    public void sign_in(View view) {
        String username = ((TextView) findViewById(R.id.Username)).getText().toString();
        String password = ((TextView) findViewById(R.id.Password)).getText().toString();
        password = AESEncrypt(password);
        String message = "SGNIN~" + username + "~" + password;
        send_message(message);
    }

    @RequiresApi(api = Build.VERSION_CODES.O)
    public String AESEncrypt(String data) {
        String value = null;
        try {
            Key keySpec = new SecretKeySpec(Key, "AES");
            @SuppressLint("GetInstance") Cipher c = Cipher.getInstance("AES");
            c.init(Cipher.ENCRYPT_MODE, keySpec);
            byte[] textEncrypted = c.doFinal(data.getBytes());
            value = Base64.getEncoder().encodeToString(textEncrypted);
            return value;
        } catch (NoSuchPaddingException | IllegalBlockSizeException | NoSuchAlgorithmException | BadPaddingException | InvalidKeyException e) {
            e.printStackTrace();
        }
        return value;
    }
}