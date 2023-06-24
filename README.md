# YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini
Digital Airlines Information System

Περιγραφή της Εφαρμογής

Υλοποιήθηκε ένα web service με χρήση Python και του Microframework Flask, το οποίο συνδέεται με ένα container της MongoDB και δίνει την δυνατότητα στους χρήστες να εκτελέσουν τις λειτουργίες που θα δούμε στην συνέχεια.

Containerize του Web service 

Αρχικά για να γίνει το containerization χρειαζόμαστε στο app.py εγκατεστημένα τα:

•	Python3 

•	Τις βιβλιοθήκες python, flask και pymongo

Δημιουργούμε το Dockerfile και στην συνέχεια δημιουργούμε το αρχείο docker-compose.yml, το οποίο συνδέει τα container web service και MongoDB ώστε να τρέχουν μαζί.

Στο terminal γράφουμε τη παρακάτω εντολή για να εισάγουμε τα users/flights/bookings.json στις collections users/flights/bookings της βάσης airlines.

Αρχικά κάνουμε copy τα δεδομένα από τον host στο container:

docker cp users.json mongodb:/users.json

docker cp flights.json mongodb:/flights.json

docker cp bookings.json mongodb:/bookings.json

Έπειτα εκτελούμε την παρακάτω εντολή για να κάνουμε import στη airlines τα 3 αρχεία.

docker exec -it mongodb mongoimport --db=airlines --collection=users --file=users.json

docker exec -it mongodb mongoimport --db=airlines --collection=flights --file=flights.json

docker exec -it mongodb mongoimport --db=airlines --collection=bookings --file=bookings.json


Web Service – Endpoints Απλού χρήστη


Signup():

Δημιουργείται ένας νέος χρήστης στο σύστημα με την μέθοδο POST. Τα στοιχεία του χρήστη που απαιτούνται για το signup θα δοθούν σε ένα json αρχείο της μορφής:


 ![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/19692a78-b08d-4328-9cfe-7900458eb167)


Σε περίπτωση που έχει ξεχαστεί κάποιο στοιχείο, το πρόγραμμα θα ενημερώσει τον χρήστη για ελλιπείς στοιχεία (“Information incomplete”).
Αν υπάρχει χρήστης με το ίδιο email ή username, τότε θα εμφανιστεί το κατάλληλο μήνυμα λάθους.


 ![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/4036762a-f4bd-4684-a052-c47ca7a7e644)



Login()

Ο χρήστης κάνει login στην υπηρεσία με την μέθοδο POST. 
Για να γίνει το login ο χρήστης πρέπει να εισάγει το email και το password του. Άμα υπάρχει τέτοιος user με το email (που είναι μοναδικό) και τον αντίστοιχο κωδικό, τότε γίνεται επιτυχημένα το login και προστίθεται στο session το username του χρήστη.


![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/d6c55ebd-7b3d-4f5f-b500-e3b0f8457b10)


 
Επίσης γίνεται έλεγχος για το άμα έχει ήδη γίνει login στο σύστημα. 
Σε περίπτωση που τα στοιχεία δεν αντιστοιχούν με κάποιον καταγεγραμμένο user εμφανίζεται το παρακάτω μήνυμα:

 ![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/622f61bd-486c-4e45-8e9b-43c38731b385)



Logout()

Ο χρήστης με την μέθοδο POST κάνει logout από το σύστημα και τελειώνει το session του.


searchFlights() 

Ο χρήστης με την μέθοδο GET, μπορεί να κάνει αναζήτηση πτήσεων. Αυτό μπορεί να γίνει: 
•	δίνοντας το αεροδρόμιο προέλευσης και το αεροδρόμιο προορισμού ή
•	το αεροδρόμιο προέλευσης, το αεροδρόμιο προορισμού και την ημερομηνία διεξαγωγής πτήσης ή
•	την διεξαγωγή πτήσης ή 
•	χωρίς arguments, όπου το σύστημα δείχνει όλες τις πτήσεις
Ο χρήστης δίνει τα ορίσματα από το URL, τα διαβάσει το πρόγραμμα και ανάλογα με τα ορίσματα που διάβασε εμφανίζει τις αντίστοιχες πτήσεις.

 
![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/0f965110-8ebe-4d89-a931-1d864902065d)



Χωρίς arguments εμφανίζονται όλες οι πτήσεις:


![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/f38dd5ba-2897-490c-b414-6b320a83bb99)


 
getFlightDet()

Εδώ χρησιμοποιείται η μέθοδος GET, όπου ο χρήστης εισάγοντας τον μοναδικό κωδικό πτήσης (_id) παίρνει τα στοιχεία της συγκεκριμένης πτήσης.


![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/2d397b4e-08b2-42fa-ba82-aa97ee16e465)

 


bookTick()

Η μέθοδος που χρησιμοποιείται εδώ είναι η POST. Ο χρήστης κάνει κράτηση ενός εισιτηρίου, βάζοντας πάλι στο  URL τον μοναδικό κωδικό (_id) της πτήσης που θέλει.


![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/ada9104b-0cfc-4f15-8f3a-ff78ba0a2f88)


 
Επίσης ο αριθμός των διαθέσιμων εισιτηρίων (business στο δικό μας παράδειγμα) στην συγκεκριμένη πτήση μειώνεται κατά 1.


![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/c2997c04-5835-4827-ba27-69c082028268)


 
Είναι σημαντικό επίσης ο χρήστης που κάνει την κράτηση να υπάρχει και να ταιριάζει με τα καταχωρημένα στοιχεία που υπάρχουν στην βάση.


![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/c4e91f16-4a55-4255-a79b-7243d878c1a5)


 
Βλέπουμε ότι δεν υπάρχει χρήστης που να ταιριάζουν αυτά τα στοιχεία ( αντί για το επίθετο ‘’Ravanopoulou’’ έχουμε το επίθετο ‘’Tomazani’’).


getBookings()

H μέθοδος που χρησιμοποιείται εδώ είναι η GET. Ο χρήστης εισάγει το email του και λαμβάνει όλες τις κρατήσεις που έχει κάνει.


![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/259c3be6-d899-43cd-b9d8-810906c14c58)

 

Πάλι γίνεται έλεγχος για το άμα αυτό το email ανήκει σε κάποιον καταχωρημένο χρήστη.


getBookingDet()

Εδώ πάλι χρησιμοποιείται η μέθοδος GET. Ο χρήστης θέλει να εμφανιστούν τα στοιχεία της κράτησης του. Αυτό πραγματοποιείται βάζοντας στο URL το μοναδικό _id της κράτησης.


![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/3d533c8b-abc9-49fd-8512-1228b0782d5e)

 


deleteBooking()

Χρησιμοποιείται η μέθοδος DELETE. Ο χρήστης για να διαγράψει μία κράτηση πρέπει να εισάγει το μοναδικό κωδικό κράτησης (_id) στο URL.
 


![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/3977ff37-73fd-4125-acb1-9fbfc2664491)




Τα διαθέσιμα εισιτήρια της πτήσης ανανεώνονται ανάλογα με τον τύπο του εισιτηρίου που είχε γίνει η κράτηση. Για παράδειγμα, η κράτηση ήταν για ένα εισιτήριο business class για την πτήση που πάει CFU.
 

![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/f9cf86c1-0cf6-45ef-8b27-51c642221fce)




deleteUser()

Γίνεται διαγραφή του χρήστη από το σύστημα με την μέθοδο DELETE. Ο χρήστης εισάγει το email και το password του και διαγράφεται από το σύστημα. Οι κρατήσεις εισιτηρίων δεν επηρεάζονται.
 


![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/c5c674cd-b879-4d44-bbc2-9c21e4ace1c7)




Web service – Endpoints διαχειριστή 

Ένας απλός χρήστης δεν μπορεί να έχει πρόσβαση σε καμία υπηρεσία που αφορά τους διαχειριστές.


createNewFlight()

Ο διαχειριστής μπορεί να δημιουργήσει μία νέα πτήση εισάγοντας τα στοιχεία που βλέπουμε στην παρακάτω εικόνα. 


![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/b13be541-821c-441c-b162-878123b08625)


 
Επίσης, πρέπει ο αριθμός των διαθέσιμων εισιτηρίων και του κόστους τους να είναι >= 0 .



![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/a367ca53-32cb-4777-86ac-e9c2a04fec1a)




updateValue()

Ο διαχειριστής μπορεί να ανανεώσει τις τιμές των εισιτηρίων βάζοντας στο URL τον μοναδικό κωδικό πτήσης (_id).


![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/910e1211-bd56-49c0-b18d-8b7225c9d657)



Γίνεται επίσης έλεγχος για τις τιμές να είναι >= 0. 


deleteFlight()

Ο διαχειριστής μπορεί να διαγράψει μια πτήση χρησιμοποιώντας στο URL τον μοναδικό κωδικό πτήσης μόνο άμα δεν υπάρχει κράτηση.



![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/9266f6c6-a275-4758-ae6f-e4db8e705897)


 
Παράδειγμα με πτήση που έχει κράτηση:


![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/5bf4a609-1c9e-4a5c-8cdf-c3f89d5d1e6f)




 
searchFlights()

Ένας διαχειριστής θα μπορεί να αναζητήσει τις πτήσεις που υπάρχουν στο σύστημα. Η αναζήτηση θα μπορεί να γίνει βάσει των παρακάτω στοιχείων: 
•	Αεροδρόμιο προέλευσης και αεροδρόμιο τελικού προορισμού, ή 
•	Αεροδρόμιο προέλευσης, αεροδρόμιο τελικού προορισμού και ημερομηνία διεξαγωγής, ή 
•	Ανά ημερομηνία, ή 
•	Εμφάνιση όλων των διαθέσιμων πτήσεων 
Θα εμφανίζεται μια λίστα με τις διαθέσιμες πτήσεις, τους μοναδικούς κωδικούς τους (_id), την ημερομηνία διεξαγωγής τους, προέλευση και τελικό προορισμό.
Ακριβώς όπως γίνεται και στους χρήστες.
 


![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/c408aa95-27bb-4ad7-a1d1-a5ee62bdf773)




getFlightDet()

Ο διαχειριστής αναζητεί μία πτήση βάση του _id της και εμφανίζονται τα παρακάτω στοιχεία.


![image](https://github.com/MagdaToma8/YpoxreotikiErgasia23_e20160_Tomazani_Maria-Magdalini/assets/128919446/0257faca-b8ed-4cf8-9869-06c637f213e4)

 
