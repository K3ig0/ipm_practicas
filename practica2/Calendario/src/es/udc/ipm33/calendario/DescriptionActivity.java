package es.udc.ipm33.calendario;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.widget.TextView;

public class DescriptionActivity extends Activity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_description);
		
		Intent intent = getIntent();
	    String event =  intent.getStringExtra(MainActivity.EXTRA_MESSAGE);
	    
	    TextView texto = (TextView) findViewById(R.id.description);
	    
	    texto.setText(event);
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.description, menu);
		return true;
	}

}
