"use client";

import React from "react";

interface DateTimeDisplayProps {
  datetime: string;
  label: string;
}

export default function DateTimeDisplay({ datetime, label }: DateTimeDisplayProps) {
  const locale = "nb-NO";
  const timeZone = "Europe/Oslo";

  const dateOptions: Intl.DateTimeFormatOptions = {
    timeZone,
    dateStyle: "short",
    timeStyle: "short",
  };

  const formattedDate = new Date(datetime).toLocaleString(locale, dateOptions);

  return (
    <p>
      {label}: {formattedDate}
    </p>
  );
}
