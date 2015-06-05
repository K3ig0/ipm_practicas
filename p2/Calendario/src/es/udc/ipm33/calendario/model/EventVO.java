package es.udc.ipm33.calendario.model;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

import org.ektorp.support.Entity;
import org.ektorp.support.TypeDiscriminator;

import android.annotation.SuppressLint;

/**
 * Encapsulates a document of type "User" in the CouchDB database
 * Every field in the document is mapped to an attribute in this class
 * Special fields _id and _rev are mapped by the attributes id and rev in
 * the superclass Entity
 */


/**
 * In order to distinguish your type's documents in the database the    
 * @TypeDiscriminator annotation can be used.
 *
 * In this example, all the database views have the following form:
 * function (doc) { if (doc.type == 'User') { ... } }
 */
@TypeDiscriminator("doc.type == 'Event'")
public class EventVO extends Entity {
	
	private static final long serialVersionUID = 6855043510343958660L;

	@SuppressLint("SimpleDateFormat")
	final SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");
    
    private String type = "Event";
    
    private String creator;
    
    private Date date;
    
    private String description;
    
    private List<String> tags;
    
    public String getType() {
        return type;
    }
        
    public void setType(String type) {
        this.type = type;
    }

    public String getCreator() {
        return creator;
    }
        
    public void setCreator(String creator) {
        this.creator = creator;
    }
    
    public String getDescription() {
        return description;
    }
        
    public void setDescription(String description) {
        this.description = description;
    }
    
    public Date getDate() {
        return date;
    }
        
    public void setDate(String date) {
    	try {
        	this.date = formatter.parse(date);
        }
        catch (ParseException e) {
        	e.printStackTrace();
        }
    }
    
    public List<String> getTags() {
        return tags;
    }
        
    public void setTags(List<String> tags) {
        this.tags = tags;
    }
    
    @Override
    public String toString() {
        String string =  this.description + "\n" + this.creator + "\n" + formatter.format(this.date) + "\n"  + this.tags.toString();
        return string;            
    }
}
