import Link from 'next/link';
import React from 'react';
import { FiSearch } from 'react-icons/fi'; // Importing a search icon from react-icons

const Hero = () => {
  return (
    <div className="flex h-screen">
      <div className="flex flex-col  place-content-center  w-full pl-[180px]  ">
        <h1 className="font-bold text-[64px] leading-[72px] max-w-[542px] pb-[20px]">
          Discover Your Next Great Read
        </h1>
        <p className="text-[#626262]  text-xl max-w-[510px] pb-[40px]">
          Browse, explore, and shop the best books for every mood and moment
        </p>
        {/* Wrapper for input and icon */}
        <div className="relative w-[580px]">
          <FiSearch className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-500 text-lg" />
          <input
            type="text"
            placeholder="Search book"
            className="border bg-[#F5F6F8] py-[12px] pl-[50px] pr-[20px] rounded-[48px] w-full text-base focus:outline-none"
          />
        </div>
      </div>
      <div
        className="w-full bg-cover bg-center flex justify-end place-items-start"
        style={{ backgroundImage: "url('/bg.jpg')" }}
      >
        <div className="text-white text-[20px] font-medium flex items-center gap-8 pt-[28px] pr-8">
          <div className="flex gap-6">
            <Link href="/" className="hover:font-bold">
              Home
            </Link>
            <Link href="#" className="hover:font-bold">
              Explore
            </Link>
            <Link href="#" className="hover:font-bold">
              Contact
            </Link>
          </div>
          <button className="bg-white text-[#F5B900] px-[24px] py-1 rounded-2xl hover:font-bold">
            Sign Up
          </button>
        </div>
      </div>
    </div>
  );
};

export default Hero;
