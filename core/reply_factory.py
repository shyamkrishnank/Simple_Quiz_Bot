
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []
    current_question_id = session.get("current_question_id")
    if current_question_id is None:
        bot_responses.append(BOT_WELCOME_MESSAGE)
        
    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    print(session['current_question_id'])
    session.save()
    print("returned bos_response",next_question_id)
    return bot_responses


def record_current_answer(answer, current_question_id, session):
    if current_question_id is None:
        session['answer_list'] = []
        session['correct_count'] = 0
        session.save()
        return True,""
    is_correct = answer == PYTHON_QUESTION_LIST[current_question_id]['answer']
    session['answer_list'].append({
        'question_id':current_question_id,
        'is_correct' : is_correct
    })
    if is_correct:
        session['correct_count'] += 1
    session.save()
    print(session['correct_count'])
    return True,""



def get_next_question(current_question_id):
    if current_question_id is not None:
         index = current_question_id + 1
    else:
         index = 0     
    if index < len(PYTHON_QUESTION_LIST):
        next_question, next_question_id = PYTHON_QUESTION_LIST[index]['question_text'], index
    else:
        next_question, next_question_id = None, index
    return next_question, next_question_id
    
         

def generate_final_response(session):
    result = f"Your test have been completed, You have scored {session['correct_count']} out of {len(PYTHON_QUESTION_LIST)}" 
    return result
