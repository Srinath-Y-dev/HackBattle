
export default function Home() {
  return (
    // The main container from your prototype
    <main className="bg-[#005f73] h-screen w-full max-w-md mx-auto flex flex-col justify-between md:max-w-lg">
      
      {/* Header section from your prototype, converted to JSX */}
      <header className="p-6 flex justify-between items-center text-white z-20">
        <button className="flex items-center space-x-3 bg-black/20 backdrop-blur-sm p-2 rounded-lg transition-transform hover:scale-105">
          {/* The icon will be fixed in the next step */}
          <i className="fas fa-treasure-chest text-amber-300 text-2xl"></i>
          <div>
            <p className="text-xs opacity-80 text-left">Total Balance</p>
            <h1 className="text-lg font-bold">₹1,24,580.75</h1>
          </div>
        </button>
        {/* We will make the toggle a component later */}
      </header>

      {/* We will build the rest of the components here */}
      <section className="flex-grow flex items-center justify-center">
        <h2 className="text-2xl text-white/50">Command Deck - Building...</h2>
      </section>

      {/* We will build the Nav component here */}
      <nav className="bg-white/90 backdrop-blur-lg w-full flex justify-around p-3 z-30 shadow-t-2xl">
        {/* Nav items will go here */}
      </nav>
    </main>
  );
}
