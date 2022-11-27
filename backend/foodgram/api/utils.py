from django.http import HttpResponse


def form_shopping_list(data):
    """Returns download link for .txt file with ingredients."""
    list_to_send = []
    for ingredient in data:
        list_to_send.append(f"{ingredient} ({data[ingredient][0]}) "
                            f"— {data[ingredient][1]}\n")
    list_to_send.append("______________________________\n"
                        "Продуктовый помощник Foodgram")
    response = HttpResponse(
        ''.join(list_to_send), content_type="text/plain; charset=utf-8"
    )
    response["Content-Disposition"] = ("attachment;"
                                       " filename='shopping_cart.txt'")
    return response
