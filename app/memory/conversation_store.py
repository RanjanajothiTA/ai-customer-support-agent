from app.database.database import get_connection
from app.memory.conversation_state import ConversationState


class ConversationStore:

    def create_conversation(
        self,
        conversation_id: str,
        customer_id: str
    ) -> ConversationState:

        connection = get_connection()

        connection.execute(
            """
            INSERT OR IGNORE INTO conversations
                (conversation_id, customer_id)
            VALUES (?, ?)
            """,
            (conversation_id, customer_id)
        )

        connection.commit()
        connection.close()

        return ConversationState(customer_id=customer_id)

    def get_conversation(
        self,
        conversation_id: str
    ) -> ConversationState | None:

        connection = get_connection()

        row = connection.execute(
            """
            SELECT customer_id, current_order_id,
                   current_issue, last_intent,
                   pending_cancellation_order_id
            FROM conversations
            WHERE conversation_id = ?
            """,
            (conversation_id,)
        ).fetchone()

        if row is None:
            connection.close()
            return None

        messages = connection.execute(
            """
            SELECT role, content
            FROM conversation_messages
            WHERE conversation_id = ?
            ORDER BY message_id
            """,
            (conversation_id,)
        ).fetchall()

        connection.close()

        return ConversationState(
            customer_id=row[0],
            current_order_id=row[1],
            current_issue=row[2],
            last_intent=row[3],
            pending_cancellation_order_id=row[4],
            messages=[
                {"role": message[0], "content": message[1]}
                for message in messages
            ]
        )

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str
    ) -> ConversationState:

        connection = get_connection()

        connection.execute(
            """
            INSERT INTO conversation_messages
                (conversation_id, role, content)
            VALUES (?, ?, ?)
            """,
            (conversation_id, role, content)
        )

        connection.commit()
        connection.close()

        state = self.get_conversation(conversation_id)

        if state is None:
            raise ValueError("Conversation not found")

        return state

    def update_context(
        self,
        conversation_id: str,
        current_order_id: str | None = None,
        current_issue: str | None = None,
        last_intent: str | None = None,
        pending_cancellation_order_id: str | None = None
    ) -> ConversationState:

        state = self.get_conversation(conversation_id)

        if state is None:
            raise ValueError("Conversation not found")

        if current_order_id is not None:
            state.current_order_id = current_order_id

        if current_issue is not None:
            state.current_issue = current_issue

        if last_intent is not None:
            state.last_intent = last_intent

        if pending_cancellation_order_id is not None:
            state.pending_cancellation_order_id = (
                pending_cancellation_order_id
            )

        connection = get_connection()

        connection.execute(
            """
            UPDATE conversations
            SET current_order_id = ?,
                current_issue = ?,
                last_intent = ?,
                pending_cancellation_order_id = ?
            WHERE conversation_id = ?
            """,
            (
                state.current_order_id,
                state.current_issue,
                state.last_intent,
                state.pending_cancellation_order_id,
                conversation_id
            )
        )

        connection.commit()
        connection.close()

        return state

    def clear_pending_cancellation(
        self,
        conversation_id: str
    ) -> ConversationState:

        connection = get_connection()

        connection.execute(
            """
            UPDATE conversations
            SET pending_cancellation_order_id = NULL
            WHERE conversation_id = ?
            """,
            (conversation_id,)
        )

        connection.commit()
        connection.close()

        state = self.get_conversation(conversation_id)

        if state is None:
            raise ValueError("Conversation not found")

        return state