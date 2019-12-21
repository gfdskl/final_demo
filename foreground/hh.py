def scene_update_view(request):
    if request.method == "POST":
            name = request.POST.get('name')
            status = 0
            result = "Error!"
            return HttpResponse(json.dumps({
                "status": status,
                "result": result
            }))
scene_update_view()