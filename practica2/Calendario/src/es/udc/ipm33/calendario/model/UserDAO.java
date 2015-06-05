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

public class UserDAO extends CouchDbRepositorySupport<UserVO> {

        public UserDAO(CouchDbConnector db) {
                super(UserVO.class, db);
                initStandardDesignDocument();
        }


        /**
         * CouchDbRepositorySupport is able to generate some views automatically.
         * Simple finder methods can be annotated with the @GenererateView annotation
         */
        @GenerateView @Override
        public List<UserVO> getAll() {
                ViewQuery q = createQuery("all")
                                .includeDocs(true);
                return db.queryView(q, UserVO.class);
        }
        
               
        @GenerateView
        public UserVO findByDescription(String description) {
            List<UserVO> users = queryView("by_description", description);
            if (users.size() == 1) {
                return  (UserVO) users.toArray()[0];
            }
            return null;
        }
        
        @GenerateView
        public List<UserVO> findBySubjects(String subject) {
            List<UserVO> users = queryView("by_subjects", subject);
            return users;        
        }
        
}
