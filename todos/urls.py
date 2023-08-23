from django.urls import path
from todos.views import TaskList,TaskDetail,TaskCreate,TaskUpdate,TaskDelete,CustomeLoginView,CustomRegisterView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', CustomeLoginView.as_view(), name="login"),
    path('register/', CustomRegisterView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(next_page='login'), name="logout"),
    path('', TaskList.as_view(), name="task-list"),
    path('task/<int:pk>', TaskDetail.as_view(), name="task-detail"),
    path('task-create', TaskCreate.as_view(), name="task-create"),
    path('task-update/<int:pk>', TaskUpdate.as_view(), name="task-update"),
    path('task-delete/<int:pk>', TaskDelete.as_view(), name="task-delete"),
]