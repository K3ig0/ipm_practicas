package es.udc.ipm33.calendario;

import java.util.List;

import android.app.Activity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;
import es.udc.ipm33.calendario.model.EventVO;

public class EventsArrayAdapter extends ArrayAdapter<EventVO> {
	private Activity context;
    private List<EventVO> events;

    public EventsArrayAdapter(Activity context, List<EventVO> events) {
        super(context, R.layout.event_row, events);
        this.context = context;
        this.events = events;
    }

    @Override
    public View getView(final int position, View contentView, ViewGroup parent) {
        View rowView = contentView;
        EventRowViewCache eventRowViewCache;

        if (rowView == null) {
            LayoutInflater inflater = context.getLayoutInflater();
            rowView = inflater.inflate(R.layout.event_row, null, true);
            eventRowViewCache = new EventRowViewCache();
            eventRowViewCache.desc = (TextView) rowView.findViewById(R.id.eventDescription);
            eventRowViewCache.tags = (TextView) rowView.findViewById(R.id.eventTag);
            rowView.setTag(eventRowViewCache);
        }
        else {
        	eventRowViewCache = (EventRowViewCache) rowView.getTag();
        }

        eventRowViewCache.desc.setText(events.get(position).getDescription());
        eventRowViewCache.tags.setText(events.get(position).getTags().toString());
        


        return rowView;
    }
    
    static class EventRowViewCache {
        public TextView desc;
        public TextView tags;
    }
}
