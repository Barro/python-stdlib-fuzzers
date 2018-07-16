import email.message
import mailbox

mail = mailbox.mbox("empty.mbox")
mail.close()
mail = mailbox.mbox("one-message.mbox")
message = email.message.Message()
message.set_payload("a")
message.add_header("h", "v", k="l")
mail.add(message)
mail.close()
