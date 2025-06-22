from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model

from lists.forms import ExistingListItemForm, ItemForm
from lists.models import Item, List


User = get_user_model()


def home_page(request):
    return render(request, "home.html", {"form": ItemForm()})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        nulist = List.objects.create()
        if request.user.is_authenticated:
            nulist.owner = request.user
            nulist.save()
        form.save(for_list=nulist)
        return redirect(nulist)
    else:
        return render(request, "home.html", {"form": form})


def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=our_list)
    if request.method == "POST":
        form = ExistingListItemForm(for_list=our_list, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(our_list)
    else:
        if (
            request.user.is_authenticated
            and request.user == our_list.owner
            or request.user in our_list.shared_with.all()
        ):
            form = ExistingListItemForm(for_list=our_list)
        else:
            return render(request, "not_allowed.html")
    return render(request, "list.html", {"list": our_list, "form": form})


def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    list = item.list
    if request.user.is_authenticated and list.owner == request.user:
        item.delete()
        if not list.item_set.all():
            list.delete()
            return redirect(f"/lists/users/{request.user.email}/")
        return redirect(list)
    return render(request, "not_allowed.html")


def my_lists(request, email):
    owner = User.objects.get(email=email)

    return render(request, "my_lists.html", {"owner": owner})


def share_list(request, list_id):
    list = List.objects.get(id=list_id)
    if request.method == "POST":
        list.shared_with.add(User.objects.get(email=request.POST["sharee_email"]))
        return redirect(list)
    return redirect(list)
