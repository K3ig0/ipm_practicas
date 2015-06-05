package es.udc.ipm33.calendario.model;

import java.util.List;

import org.ektorp.support.Entity;
import org.ektorp.support.TypeDiscriminator;

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
@TypeDiscriminator("doc.type == 'User'")
public class UserVO extends Entity {

	private static final long serialVersionUID = -2457573725354125049L;

	private String type = "User";
    
    private String subtype;
    
    private String description;
    
    private List<String> subjects;
    
    public String getType() {
        return type;
    }
        
    public void setType(String type) {
        this.type = type;
    }

    public String getSubtype() {
        return subtype;
    }
        
    public void setSubtype(String subtype) {
        this.subtype = subtype;
    }
    
    public String getDescription() {
        return description;
    }
        
    public void setDescription(String description) {
        this.description = description;
    }
    
    public List<String> getSubjects() {
        return subjects;
    }
        
    public void setSubjects(List<String> subjects) {
        this.subjects = subjects;
    }
    
    @Override
    public String toString() {
        String string = super.getId() + "@" + super.getRevision() + " | " + this.type + " | " + this.subtype  + " | " + 
            this.description + "\t| [";
        for (String subject:subjects) {
            string += subject+ ";";
        }
        string += "]";
        return string;            
    }

    

}
