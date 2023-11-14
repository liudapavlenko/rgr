import psycopg2
import time
class Model:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='Deanery',
            user='postgres',
            password='qwerty',
            host='localhost',
            port=5432
        )

    def gener_add_user(self, num1, num2):
        c = self.conn.cursor()
        num = 0
        for i in range(num1, num2+1):
            c.execute('SELECT * FROM "User" WHERE "UserID" = %s', (i,))
            check = c.fetchall()
            if check:
                print("UserID %s already exists", i)
                num = 1

        if num == 0:
            c.execute('INSERT INTO "User" ("UserID", "Name", "Surname") SELECT generate_series as UserID, chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) as Name,chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) as Surname FROM generate_series(%s, %s)', (num1, num2))
            self.conn.commit()
        else:
            print("Error! Identifiers already exist")

    #3 requests
    def request_1(self, val1, val2):
        c = self.conn.cursor()
        start_t = time.time()
        c.execute('SELECT * FROM "Composer" INNER JOIN "Notes" ON "Composer"."ComposerID" = "Notes"."ComposerID" WHERE "Composer"."Name" LIKE %s AND "NotesID" > %s group by "Composer"."ComposerID", "Notes"."NotesID";', (val1, val2))
        end_t = time.time()
        time_t = (end_t - start_t) * 1000
        print("Time 1:", time_t)
        return c.fetchall()


    def request_2(self, val1, val2):
        c = self.conn.cursor()
        start_t = time.time()
        c.execute('SELECT * FROM "Notes" INNER JOIN "Saving_notes" ON "Notes"."NotesID" = "Saving_notes"."NotesID" WHERE "Notes"."composition name" LIKE %s OR "Saving_notes"."CatalogID" > %s group by "Saving_notes"."Saving_notesID", "Notes"."NotesID"', (val1, val2))
        end_t = time.time()
        time_t = (end_t - start_t) * 1000
        print("Time 2:", time_t)
        return c.fetchall()

    def request_3(self, val1, val2):
        c = self.conn.cursor()
        start_t = time.time()
        c.execute('SELECT * FROM "Saving_notes" INNER JOIN "Notes" ON "Saving_notes"."NotesID" = "Notes"."NotesID" INNER JOIN "User" ON "Saving_notes"."UserID" = "User"."UserID" WHERE "User"."Name" LIKE %s AND "Saving_notes"."CatalogID" > %s group by "Saving_notes"."Saving_notesID", "Notes"."NotesID", "User"."UserID"', (val1, val2))
        end_t = time.time()
        time_t = (end_t - start_t) * 1000
        print("Time 3:", time_t)
        return c.fetchall()

    # for catalog
    def add_catalog(self, catalog_id, name):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Catalog" WHERE "CatalogID" = %s', (catalog_id,))
        check = c.fetchall()
        if check:
            print("Error! This identifier already exists")
        else:
            c.execute('INSERT INTO "Catalog" ("CatalogID", "catalog_name") VALUES (%s, %s)', (catalog_id, name))
            self.conn.commit()
            print("Catalog added successfully!")

    def update_catalog(self, catalog_id, catal_name):
        c = self.conn.cursor()
        c.execute('UPDATE "Catalog" SET "catalog_name"=%s WHERE "CatalogID"=%s', (catal_name, catalog_id))
        self.conn.commit()
        print("Catalog updated successfully!")

    def delete_catalog(self, catalog_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Catalog" WHERE "CatalogID" = %s', (catalog_id,))
        check1 = c.fetchall()
        c.execute('SELECT * FROM "Saving_notes" WHERE "CatalogID" = %s', (catalog_id,))
        check2 = c.fetchall()
        if check1 and check2:
            c.execute('DELETE FROM "Saving_notes" WHERE "CatalogID"=%s', (catalog_id,))
            self.conn.commit()
            c.execute('DELETE FROM "Catalog" WHERE "CatalogID"=%s', (catalog_id,))
            self.conn.commit()
            print("Catalog deleted successfully!")
        elif check1:
            c.execute('DELETE FROM "Catalog" WHERE "CatalogID"=%s', (catalog_id,))
            self.conn.commit()
            print("Catalog deleted successfully!")
        else:
            print("Error! This CatalogID not exist")


    def get_all_catalog(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Catalog"')
        return c.fetchall()

    # for user
    def add_user(self, user_id, Name, Surname):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "User" WHERE "UserID" = %s', (user_id,))
        check = c.fetchall()
        if check:
            print("Error! This identifier already exists")
        else:
            c.execute('INSERT INTO "User" ("UserID","Name", "Surname") VALUES (%s, %s, %s)', (user_id, Name, Surname))
            self.conn.commit()
            print("User added successfully!")

    def get_all_user(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "User"')
        return c.fetchall()

    def update_user(self, user_id, Name, Surname):
        c = self.conn.cursor()
        c.execute('UPDATE "User" SET "Name"=%s, "Surname"=%s WHERE "UserID"=%s', (Name, Surname, user_id))
        self.conn.commit()

    def delete_user(self, user_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "User" WHERE "UserID" = %s', (user_id,))
        check1 = c.fetchall()
        c.execute('SELECT * FROM "Saving_notes" WHERE "UserID" = %s', (user_id,))
        check2 = c.fetchall()
        if check1 and check2:
            c.execute('DELETE FROM "Saving_notes" WHERE "UserID"=%s', (user_id,))
            self.conn.commit()
            c.execute('DELETE FROM "User" WHERE "UserID"=%s', (user_id,))
            self.conn.commit()
            print("User deleted successfully!")
        elif check1:
            c.execute('DELETE FROM "User" WHERE "UserID"=%s', (user_id,))
            self.conn.commit()
            print("User deleted successfully!")
        else:
            print("Error! This UserID not exist")


    # for composer

    def add_composer(self, composer_id, Name, Surname):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Composer" WHERE "ComposerID" = %s', (composer_id,))
        check = c.fetchall()
        if check:
            print("Error! This identifier already exists")
        else:
            c.execute('INSERT INTO "Composer" ("ComposerID", "Name", "Surname") VALUES (%s, %s, %s)',(composer_id, Name, Surname))
            self.conn.commit()
            print("Composer added successfully!")

    def get_all_composer(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Composer"')
        return c.fetchall()

    def update_composer(self, composer_id, Name, Surname):
        c = self.conn.cursor()
        c.execute('UPDATE "Composer" SET "Name"=%s, "Surname"=%s WHERE "ComposerID"=%s', (Name, Surname, composer_id))
        self.conn.commit()
        print("Composer updated successfully!")

    def delete_composer(self, composer_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Composer" WHERE "ComposerID" = %s', (composer_id,))
        check1 = c.fetchall()
        c.execute('SELECT * FROM "Notes" WHERE "ComposerID" = %s', (composer_id,))
        check2 = c.fetchall()
        if check1 and check2:
            c.execute('SELECT "NotesID" FROM "Notes" WHERE "ComposerID" = %s', (composer_id,))
            n = c.fetchall()
            c.execute('DELETE FROM "Saving_notes" WHERE "NotesID"= %s', (n[0],))
            self.conn.commit()
            c.execute('DELETE FROM "Notes" WHERE "ComposerID"=%s', (composer_id,))
            self.conn.commit()
            c.execute('DELETE FROM "Composer" WHERE "ComposerID"=%s', (composer_id,))
            self.conn.commit()
            print("Composer deleted successfully!")
        elif check1:
            c.execute('DELETE FROM "Composer" WHERE "ComposerID"=%s', (composer_id,))
            self.conn.commit()
            print("Composer deleted successfully!")
        else:
            print("Error! This ComposerID not exist")

        # for notes

    def add_notes(self, notes_id, composer_id, comp_name):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Notes" WHERE "NotesID" = %s', (notes_id,))
        check2 = c.fetchall()
        if check2:
            print("Error! This identifier NotesID already exists")
        else:
            c.execute('SELECT * FROM "Composer" WHERE "ComposerID" = %s', (composer_id,))
            check1 = c.fetchall()
            if check1:
                c.execute('INSERT INTO "Notes" ("NotesID","ComposerID", "composition name") VALUES (%s, %s, %s)',(notes_id, composer_id, comp_name))
                self.conn.commit()
                print("Notes added successfully!")
            else:
                print("Error! This identifier ComposerID already exists")
    def get_all_notes(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Notes"')
        return c.fetchall()

    def update_notes(self, notes_id, composer_id, comp_name):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Composer" WHERE "ComposerID" = %s', (composer_id,))
        check = c.fetchall()
        if check:
            c.execute('UPDATE "Notes" SET "ComposerID"=%s, "composition name"=%s WHERE "NotesID"=%s',(composer_id, comp_name, notes_id))
            self.conn.commit()
            print("Notes updated successfully!")
        else:
            print("Error! The ID that was changed is not in the parent table")


    def delete_notes(self, notes_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Notes" WHERE "NotesID" = %s', (notes_id,))
        check1 = c.fetchall()
        c.execute('SELECT * FROM "Notes" WHERE "NotesID" = %s', (notes_id,))
        check2 = c.fetchall()
        if check1 and check2:
            c.execute('DELETE FROM "Saving_notes" WHERE "NotesID"=%s', (notes_id,))
            self.conn.commit()
            c.execute('DELETE FROM "Notes" WHERE "NotesID"=%s', (notes_id,))
            self.conn.commit()
            print("Notes deleted successfully!")
        elif check1:
            c.execute('DELETE FROM "Notes" WHERE "NotesID"=%s', (notes_id,))
            self.conn.commit()
            print("Notes deleted successfully!")
        else:
            print("Error! This NotesID not exist")


    #save notes
    def add_save_notes(self, save_notes_id, catalog_id, notes_id, user_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Saving_notes" WHERE "Saving_notesID" = %s', (save_notes_id,))
        check = c.fetchall()
        if check:
            print("Error! This identifier already exists")
        else:
            c.execute('SELECT * FROM "Catalog" WHERE "CatalogID" = %s', (catalog_id,))
            check1 = c.fetchall()
            c.execute('SELECT * FROM "Notes" WHERE "NotesID" = %s', (notes_id,))
            check2 = c.fetchall()
            c.execute('SELECT * FROM "User" WHERE "UserID" = %s', (user_id,))
            check3 = c.fetchall()
            if check1 and check2 and check3:
                c.execute('INSERT INTO "Saving_notes" ("Saving_notesID","CatalogID","NotesID", "UserID") VALUES (%s, %s, %s, %s)',(save_notes_id, catalog_id, notes_id, user_id))
                self.conn.commit()
                print("Notes added successfully!")
            else:
                print("Error! This identifier already exists")

    def get_all_save_notes(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Saving_notes"')
        return c.fetchall()

    def update_save_notes(self, catalog_id, notes_id, user_id, save_notes_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Catalog" WHERE "CatalogID" = %s', (catalog_id,))
        check1 = c.fetchall()
        c.execute('SELECT * FROM "Notes" WHERE "NotesID" = %s', (notes_id,))
        check2 = c.fetchall()
        c.execute('SELECT * FROM "User" WHERE "UserID" = %s', (user_id,))
        check3 = c.fetchall()
        if check1 and check2 and check3:
            c.execute('UPDATE "Saving_notes" SET "CatalogID"=%s, "NotesID"=%s, "UserID"=%s WHERE "Saving_notesID"=%s',(catalog_id, notes_id, user_id, save_notes_id))
            self.conn.commit()
            print("Saving notes updated successfully!")
        else:
            print("Error! The ID that was changed is not in the parent table")
    def delete_save_notes(self, save_notes_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Saving_notes" WHERE "Saving_notesID" = %s', (save_notes_id,))
        check = c.fetchall()
        if check:
            c.execute('DELETE FROM "Saving_notes" WHERE "Saving_notesID"=%s', (save_notes_id,))
            self.conn.commit()
            print("Saving notes deleted successfully!")
        else:
            print("Error! Saving notes ID not exist")
