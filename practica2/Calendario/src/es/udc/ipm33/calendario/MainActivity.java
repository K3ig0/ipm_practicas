package es.udc.ipm33.calendario;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.LinkedList;
import java.util.List;

import org.ektorp.CouchDbConnector;
import org.ektorp.DbAccessException;
import org.ektorp.android.util.EktorpAsyncTask;

import android.app.AlertDialog;
import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.FragmentTransaction;
import android.support.v4.app.NotificationCompat;
import android.text.InputType;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Spinner;
import android.widget.Toast;

import com.roomorama.caldroid.CaldroidFragment;
import com.roomorama.caldroid.CaldroidListener;

import es.udc.ipm33.calendario.model.CouchDBAndroidHelper;
import es.udc.ipm33.calendario.model.EventDAO;
import es.udc.ipm33.calendario.model.EventVO;
import es.udc.ipm33.calendario.model.UserDAO;
import es.udc.ipm33.calendario.model.UserVO;


public class MainActivity extends FragmentActivity {
	private CaldroidFragment caldroidFragment;
	private List<EventVO> dailyEvents = new LinkedList<EventVO>();
	private ArrayAdapter<EventVO> eventsListViewAdapter;
	private ProgressDialog progressDialog;
	private List<String> subjects;
	MenuItem menuViewBySubject;
    MenuItem menuLogout;
    MenuItem menuLogin;
    public final static String EXTRA_MESSAGE = "es.udc.ipm33.calendario.MESSAGE";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        // Configure bottom list view
        ListView eventListView = (ListView) findViewById(R.id.eventList);
        eventsListViewAdapter = new EventsArrayAdapter(this, dailyEvents);
        eventListView.setAdapter(eventsListViewAdapter);

        eventListView.setOnItemClickListener(new OnItemClickListener() {
            public void onItemClick(AdapterView<?> parent, View view,int position, long id) {
				Intent i = new Intent(MainActivity.this, DescriptionActivity.class);
				i.putExtra(EXTRA_MESSAGE, dailyEvents.get(position).toString());
				
				startActivity(i);
            }
          });
        
        if (savedInstanceState != null) {
    	  caldroidFragment.restoreStatesFromKey(savedInstanceState, "CALDROID_SAVED_STATE");
    	} 
        else {
        // Configure calendar view        
	        caldroidFragment = new CaldroidFragment();
	        Bundle args = new Bundle();
	        Calendar cal = Calendar.getInstance();
	        args.putInt(CaldroidFragment.MONTH, cal.get(Calendar.MONTH) + 1);
	        args.putInt(CaldroidFragment.YEAR, cal.get(Calendar.YEAR));
	        args.putInt(CaldroidFragment.START_DAY_OF_WEEK, CaldroidFragment.MONDAY);
	        caldroidFragment.setArguments(args);
    	}
        
        FragmentTransaction t = getSupportFragmentManager().beginTransaction();
        t.replace(R.id.calendar1, caldroidFragment);
        t.commit();
        
        updateBySubject(null);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        menuViewBySubject = menu.findItem(R.id.menu_view_by_subject);
        menuLogout = menu.findItem(R.id.menu_logout);
        menuLogin = menu.findItem(R.id.menu_login);
        
        menuViewBySubject.setVisible(false); // hide until login
        menuLogout.setVisible(false); // hide until login

        return true;
    }
    
    public boolean onOptionsItemSelected(MenuItem item) {
		switch (item.getItemId()) {
			case R.id.menu_login:
				AlertDialog.Builder builder = new AlertDialog.Builder(this);
				builder.setTitle(R.string.menu_login);
	
				final EditText input = new EditText(this);
				input.setInputType(InputType.TYPE_CLASS_TEXT);
				builder.setView(input);
	
				builder.setPositiveButton(R.string.ok, new DialogInterface.OnClickListener() { 
				    @Override
				    public void onClick(DialogInterface dialog, int which) {
				        String user = input.getText().toString();
				        updateByUser(user);
				    }
				});
				builder.setNegativeButton(R.string.cancel, new DialogInterface.OnClickListener() {
				    @Override
				    public void onClick(DialogInterface dialog, int which) {
				        dialog.cancel();
				    }
				});
	
				builder.show();
				break;
				
			case R.id.menu_view_by_subject:
				AlertDialog.Builder builder2 = new AlertDialog.Builder(this);
				builder2.setTitle(R.string.select_subject);
	
				final Spinner spinner = new Spinner(this);
				builder2.setView(spinner);
				
				ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, subjects);
				spinner.setAdapter(adapter);
				
				builder2.setPositiveButton(R.string.ok, new DialogInterface.OnClickListener() { 
				    @Override
				    public void onClick(DialogInterface dialog, int which) {
				        List<String> subject = new ArrayList<String>(1);
				        subject.add(spinner.getSelectedItem().toString());
				        updateBySubject(subject);
				    }
				});
				builder2.setNegativeButton(R.string.cancel, new DialogInterface.OnClickListener() {
				    @Override
				    public void onClick(DialogInterface dialog, int which) {
				        dialog.cancel();
				    }
				});
	
				builder2.show();
				break;
			
			case R.id.menu_logout:
				updateBySubject(null);
				menuViewBySubject.setVisible(false); // hide until login
		        menuLogout.setVisible(false); // hide until login
		        menuLogin.setVisible(true); // show login again
		        break;
		}
			
    	return false;
    }
    
    private void updateByUser(final String user) {
    	progressDialog = new ProgressDialog(MainActivity.this);
        progressDialog.setTitle(getString(R.string.loading));
        progressDialog.setMessage(getString(R.string.loading_user));
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.show();
    	EktorpAsyncTask getUsersTask = new EktorpAsyncTask() {
    		
    		private UserVO result = null;
    		
            @Override
            protected void doInBackground() {
                CouchDBAndroidHelper dbHelper = CouchDBAndroidHelper.getInstance();
                CouchDbConnector connector = dbHelper.getDbConnector();
                UserDAO userDAO = new UserDAO(connector);
                result = userDAO.findByDescription(user);
            }

            @Override
            protected void onSuccess() {
            	progressDialog.dismiss(); // dismiss first because here another dialog will be shown
            	if (result != null) {
            		subjects = result.getSubjects();
            		updateBySubject(result.getSubjects());
                    menuLogout.setVisible(true);
                    menuLogin.setVisible(false);
                    if (result.getSubtype().equals("teacher"))
                    	menuViewBySubject.setVisible(true);
            	} else {
            		Toast.makeText(getApplicationContext(), R.string.invalid_username, Toast.LENGTH_LONG).show();
            	}
            }

            @Override
            protected void onDbAccessException(DbAccessException dbAccessException) {
            	progressDialog.dismiss();
                Log.e("Calendar/MainActivity", "DbAccessException in background", dbAccessException);
                Toast.makeText(getApplicationContext(), R.string.connection_error, Toast.LENGTH_LONG).show();
            }
        };
        getUsersTask.execute();
    }
    
    private void updateBySubject(final List<String> subjects) {
    	progressDialog = new ProgressDialog(MainActivity.this);
        progressDialog.setTitle(getString(R.string.loading));
        progressDialog.setMessage(getString(R.string.loading_events));
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.show();
        
    	// Get and mark event days
        EktorpAsyncTask getEventsTask = new EktorpAsyncTask() {
        	
        	private List<EventVO> events = null;
        	
            @Override
            protected void doInBackground() {
                CouchDBAndroidHelper dbHelper = CouchDBAndroidHelper.getInstance();
                CouchDbConnector connector = dbHelper.getDbConnector();
                EventDAO eventDAO = new EventDAO(connector);
                events = eventDAO.getAll();
            }

            @Override
            protected void onSuccess() {
            	caldroidFragment.setBackgroundResourceForDates(null);
            	for (EventVO event:events) {
    				if (subjects == null || subjects.contains(event.getTags().get(0))) {
    					if (Math.abs(event.getDate().getTime() - new Date().getTime()) < 86400000*3)
    						showNotification(event);
    					caldroidFragment.setBackgroundResourceForDate(R.color.blue, event.getDate());
    				}
            	}
            	// refresh view and clear list after change marked days
            	caldroidFragment.refreshView();
            	dailyEvents.clear();
    	    	eventsListViewAdapter.notifyDataSetChanged();
            	progressDialog.dismiss();
            	
            	final CaldroidListener listener = new CaldroidListener() {

            	    @Override
            	    public void onSelectDate(Date date, View view) {
            	    	dailyEvents.clear();
                    	for (EventVO event:events) {
                    		if (event.getDate().equals(date) && (subjects == null || subjects.contains(event.getTags().get(0)))) {
                    			dailyEvents.add(event);
                    		}
                    	}
                    	eventsListViewAdapter.notifyDataSetChanged();
            	    }
            	    
            	    @Override
            	    public void onChangeMonth(int month, int year) {
            	    	// on change month clean event descriptions 'cause no longer valid for new month
            	    	dailyEvents.clear();
            	    	eventsListViewAdapter.notifyDataSetChanged();
            	    }
            	};
            	
            	caldroidFragment.setCaldroidListener(listener);
            }

            @Override
            protected void onDbAccessException(DbAccessException dbAccessException) {
            	progressDialog.dismiss();
                Log.e("Calendar/MainActivity", "DbAccessException in background", dbAccessException);
                Toast.makeText(getApplicationContext(), R.string.connection_error, Toast.LENGTH_LONG).show();
            }
        };
        getEventsTask.execute();
    }
    
    private void showNotification(EventVO event) {
		Intent intent = new Intent(this, DescriptionActivity.class);
		intent.putExtra(EXTRA_MESSAGE, event.toString());
		intent.setAction(Long.toString(System.currentTimeMillis()));
		PendingIntent pIntent = PendingIntent.getActivity(this, 0, intent, PendingIntent.FLAG_UPDATE_CURRENT);
		
		Notification n  = new  NotificationCompat.Builder(this)
		        .setContentTitle(getString(R.string.close_event))
		        .setContentText(event.getDescription() + " " + event.getTags().toString())
		        .setSmallIcon(R.drawable.ic_launcher)
		        .setContentIntent(pIntent)
		        .setAutoCancel(true).build();
		    
		  
		NotificationManager notificationManager = 
		  (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
		
		notificationManager.notify(event.hashCode(), n); 
    }
    
    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);

        if (caldroidFragment != null) {
            caldroidFragment.saveStatesToKey(outState, "CALDROID_SAVED_STATE");
        }
    }
}
