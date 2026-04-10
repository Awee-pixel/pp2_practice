CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE user_name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE user_name = p_name;
    ELSE
        INSERT INTO contacts(user_name, phone) VALUES(p_name, p_phone);
    END IF;
END;$$;

CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    p_names VARCHAR[], 
    p_phones VARCHAR[], 
    INOUT p_invalid_entries TEXT[] DEFAULT '{}'
)
LANGUAGE plpgsql AS $$DECLARE
    i INT;
    curr_phone VARCHAR;
BEGIN
    p_invalid_entries := '{}'; -- Очищаем массив вывода
    FOR i IN 1 .. array_length(p_names, 1) LOOP
        curr_phone := p_phones[i];
        IF curr_phone ~ '^\+?[0-9]{9,14}$' THEN
            INSERT INTO contacts(user_name, phone) VALUES(p_names[i], p_phones[i]);
        ELSE
            p_invalid_entries := array_append(p_invalid_entries, p_names[i] || ' -> ' || p_phones[i]);
        END IF;
    END LOOP;
END;$$;

CREATE OR REPLACE PROCEDURE delete_contact(p_val VARCHAR)
LANGUAGE plpgsql AS $$BEGIN
    DELETE FROM contacts
    WHERE user_name = p_val OR phone = p_val;
END;$$;