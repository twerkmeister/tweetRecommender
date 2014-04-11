import java.util.Arrays;

import com.mongodb.BasicDBObject;
import com.mongodb.BasicDBObjectBuilder;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBCursor;
import com.mongodb.DBObject;
import com.mongodb.ServerAddress;
import com.mongodb.MongoClient;
import com.mongodb.MongoCredential;
import com.mongodb.MongoException;
import com.mongodb.WriteConcern;

import de.l3s.boilerpipe.extractors.ArticleExtractor;

public class MongoBoilerpipe {
    static String ID = "_id";

    public static void main (final String [] args) throws Exception
    {
        if (args.length != 7) {
            System.out.println("MongoBoilerpipe <host> <username> <password> <database> <source collection> <target collection> <key>");
            System.exit(1);
        }
        final String host = args[0];
        final String username = args[1];
        final String password = args[2];
        final String db = args[3];
        final String source_table = args[4];
        final String target_table = args[5];
        final String key = args[6];
        MongoClient mongo = new MongoClient(host);
        mongo.setWriteConcern(WriteConcern.UNACKNOWLEDGED);
        DB connection = mongo.getDB(db);
        connection.authenticate(username, password.toCharArray());
        DBCollection from_collection = connection.getCollection(source_table);
        DBCollection to_collection = connection.getCollection(target_table);
        DBCursor cursor = from_collection.find(
            new BasicDBObject(key, new BasicDBObject("$exists", 1)));
        for (DBObject doc : cursor) {
            Object id = doc.get(ID);
            if (to_collection.findOne(new BasicDBObject(ID, id)) != null) {
                continue;
            }
            String original = (String) doc.get(key);
            String boilerpiped = ArticleExtractor.INSTANCE.getText(original);
            doc.put(key, boilerpiped);
            to_collection.save(doc);
        }
    }
}
