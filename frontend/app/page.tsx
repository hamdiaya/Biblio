'use client'
import Hero from "@/components/hero";
import Image from "next/image";
import PopularBooks from "@/components/popularBooks";
import { useEffect, useState } from "react";
import axios from "axios";
export default function Home() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    // Fetch popular books
    const fetchBooks = async () => {
      try {
        const response = await axios.get("https://biblio-stht.onrender.com/get10TopBooks");
        setBooks(response.data); 
        console.log(response.data);
        setLoading(false);
      } catch (err) {
        console.log(err)
        setError("Failed to fetch popular books.");
        setLoading(false);
      }
    };

    fetchBooks();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        {/* Loading Spinner */}
        <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-[#F5B900]"></div>
      </div>
    );
  }
  if (error) return <p>{error}</p>;

  return (
    <div>
      <Hero/>
      <PopularBooks books={books}/>
    </div>
      );
}
