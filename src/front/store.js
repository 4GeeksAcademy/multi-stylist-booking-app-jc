export const initialStore = () => {
  const getProvider = () => {
    try {
      const providerString = localStorage.getItem("provider");
      if (!providerString || providerString === "undefined") {
        return null;
      }

      return JSON.parse(providerString);
    } catch (error) {
      console.error("Error parsing provider from data", error);
      return null;
    }
  };
  return {
    provider: getProvider(),
  };
};

export default function storeReducer(store, action = {}) {
  switch (action.type) {
    case "login-provider":
      const { provider, token } = action.payload;
      return {
        ...store,
        provider,
        token,
      };

    default:
      throw Error("Unknown action.");
  }
}
