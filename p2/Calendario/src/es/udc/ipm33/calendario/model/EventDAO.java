package es.udc.ipm33.calendario.model;

import java.util.List;

import org.ektorp.CouchDbConnector;
import org.ektorp.ViewQuery;
import org.ektorp.support.CouchDbRepositorySupport;
import org.ektorp.support.GenerateView;

/**
 * The Repository Support in Ektorp is aimed to reduce the amount of repetitive 
 * code in repositories and to facilitate the management of the design documents
 * that define the views for the documents in CouchDB.
 *
 * Ektorp provides a repository base class org.ektorp.support.CouchDbRepositorySupport 
 * that has a number of features:
 * 
 * - Out of the box CRUD (add/remove/update/get/getAll/contains functions)
 * - Automatic view generation (@GenerateView)
 * - View management (in-line view definitions)
 */

public class EventDAO extends CouchDbRepositorySupport<EventVO> {

        public EventDAO(CouchDbConnector db) {
                super(EventVO.class, db);
                initStandardDesignDocument();
        }


        /**
         * CouchDbRepositorySupport is able to generate some views automatically.
         * Simple finder methods can be annotated with the @GenererateView annotation
         */
        @GenerateView @Override
        public List<EventVO> getAll() {
                ViewQuery q = createQuery("all")
                                .includeDocs(true);
                return db.queryView(q, EventVO.class);
        }
        
               
        @GenerateView
        public List<EventVO> findByDate(String date) {
            List<EventVO> events = queryView("by_date", date);
            return events;
        }
        
        @GenerateView
        public List<EventVO> findByTags(String tag) {
            List<EventVO> events = queryView("by_tags", tag);
            return events;        
        }
        
}
