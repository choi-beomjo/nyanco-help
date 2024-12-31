import { useRouter } from "vue-router";

export function useRouterActions(basePath) {
  const router = useRouter();

  const goBack = () => {
    router.push("/");
  };

  const goToEdit = (id) => {
    router.push(`/${basePath}/edit/${id}`);
  };

  const goAdd = () => {
    router.push(`/${basePath}/add`);
  };

  return {
    goBack,
    goToEdit,
    goAdd,
  };
}
